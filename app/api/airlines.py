from http.client import HTTPException
from statistics import mean
from typing import Optional
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from app.data.quantities import available_quantities_list
from app.data.param_columns import param_to_column
from fastapi.encoders import jsonable_encoder
from app import schemas
import pandas as pd
import json
from app.schemas.stat_details import StatsResponse


router = APIRouter()

airlines_df = pd.DataFrame()


class UnprocessableEntityException(HTTPException):
    pass


def unprocessable_entity_exception_handler(ex: UnprocessableEntityException, errors: list[str]):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"errors": f"{errors}"}
    )


class NotFoundException(HTTPException):
    pass


def not_found_exception_handler(ex: NotFoundException, errors: list[str]):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"errors": f"{errors}"}
    )


def get_stats(year: int, code: str, param: str, unit: str, decimal_places: int, summary_type: str) -> StatsResponse:
    """
    Returns airport stats for an airport during a given year
    """
    relevant_airports_df = airlines_df.loc[(airlines_df["Airport.Code"] == code.upper()) & (airlines_df["Time.Year"] == year)]

    # Set monthly data
    monthly_data = [None for _ in range(12)]
    for _, row in relevant_airports_df.iterrows():
        index = row["Time.Month"] - 1
        if summary_type == "total":
            monthly_data[index] = row[param_to_column[param]]
        else:
            monthly_data[index] = round((row[param_to_column[param]] / row["Statistics.Flights.Total"]) * 100, decimal_places)

    # Set summary
    summary: int | float
    if summary_type == "total":
        summary = sum(monthly_data)
    else:
        summary = round(mean(monthly_data), decimal_places)

    return StatsResponse(monthly_data=monthly_data, summaryType=summary_type, unit=unit, summary=summary)


@router.get("")
def verify_app():
    """
    Verify that the app is running @
    http://localhost:8000/api/airlines
    """
    return "Hello world!"


@router.get("/available-airport-codes")
def available_codes():
    """
    Returns a Json array of all available airport codes in the dataset
    """
    global airlines_df

    # Check if the airline data is cached, otherwise request the data and cache it
    if airlines_df.empty:
        with open("app\\data\\airlines.json") as airlines_json:
            airlines_data = json.load(airlines_json)

            airlines_df = pd.json_normalize(airlines_data)

    return jsonable_encoder(set(airlines_df["Airport.Code"]))


@router.get("/available-years")
def available_years():
    """
    Returns a Json array of all available years in the dataset
    """
    global airlines_df

    # Check if the airline data is cached, otherwise request the data and cache it
    if airlines_df.empty:
        with open("app\\data\\airlines.json") as airlines_json:
            airlines_data = json.load(airlines_json)

            airlines_df = pd.json_normalize(airlines_data)

    return jsonable_encoder(set(airlines_df["Time.Year"]))


@router.get("/available-quantities", response_model=list[schemas.QuantityResponse])
def available_quantities():
    """
    Returns a Json array of all available quantities in the dataset
    """
    return available_quantities_list


@router.get("/annual-statistics/{year}", response_model=list[schemas.StatsResponse])
def annual_statistics(year: int, quantities: str, airport_codes: Optional[str] = Query(None, alias="airport-codes")):
    """
    Returns a Json array of annual statistics about all available
    airports, or those specified in the airport_codes query
    """
    errors = []

    # Check for 422 errors
    # Check if year 4 digits long
    if len(str(year)) != 4:
        errors.append("Year should be a 4 digit integer")

    # Check format for airport codes (if requested)
    codes = []
    if airport_codes != None:
        codes = airport_codes.split(",")
        for code in codes:
            if len(code) != 3:
                errors.append("Airport codes should 3 characters long and seperated by commas")

    if errors:
        raise UnprocessableEntityException(errors)

    # Check for 404 errors
    # Check if year is in available-years
    if year not in available_years():
        errors.append(f"Requested year ({year}) is not available")

    # Check if airport code is in available-codes
    for code in codes:
        if code.upper() not in available_codes():
            errors.append(f"Requested code ({code}) is not available")
    
    # Check if quantity is in available-quantities
    quantities = quantities.split(",")
    available_params = list(map(lambda body: body.param, available_quantities()))
    for item in quantities:
        if item not in available_params:
            errors.append(f"Requested quantity ({item}) is not available")

    if errors:
        raise NotFoundException(errors)

    # If airport-codes is not specified, get stats on all airports
    # Otherwise get the stats for those requested
    if not codes:
        codes = available_codes()

    response = []
    for code in codes:
        for quantity in quantities:
            for item in available_quantities():
                if item.param == quantity:
                    response.append({code.upper(): {item.param: get_stats(
                        year=year, 
                        code=code,
                        param=item.param, 
                        unit=item.unit, 
                        decimal_places=item.decimal_places, 
                        summary_type=item.summaryType)}})
            

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"annual-statistics": jsonable_encoder(response)})
    
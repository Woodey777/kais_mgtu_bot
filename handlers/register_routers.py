# from survey_handler import test_survey
from .start_router import start_router
from .cardio_router import cardio_router

def register_routers(dp):
    dp.include_router(start_router)
    dp.include_router(cardio_router)

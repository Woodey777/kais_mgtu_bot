# from survey_handler import test_survey
from .start_router import start_router
from .activity_router import activity_router

def register_routers(dp):
    dp.include_router(start_router)
    dp.include_router(activity_router)

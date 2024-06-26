from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(usecwd=True))


class Config(BaseSettings):
    # kafka_topic: str = os.environ['KAFKA_TOPIC']
    # kafka_broker_address: str = os.environ['KAFKA_BROKER_ADDRESS']
    # hopsworks_project_name: str = os.environ['HOPSWORKS_PROJECT_NAME']
    # hopsworks_api_key: str = os.environ['HOPSWORKS_API_KEY']
    # feature_group_name: str = os.environ['FEATURE_GROUP_NAME']
    # feature_group_version: int = int(os.environ['FEATURE_GROUP_VERSION'])

    kafka_broker_address: str = 'localhost:19092'  # default to local broker address
    kafka_topic: str
    hopsworks_project_name: str
    hopsworks_api_key: str
    feature_group_name: str
    feature_group_version: int
    buffer_size: int = 1


# Load configuration from environment variables
config = Config()  # pyright: ignore

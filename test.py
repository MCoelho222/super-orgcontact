import os
import json

test = os.getenv('FLASK_ENV')

if __name__ == "__main__":
    print(test)
    print(json.dumps(test))
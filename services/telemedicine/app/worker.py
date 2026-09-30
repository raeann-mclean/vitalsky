"""Placeholder async worker.

In AWS, this process can consume SQS messages and invoke long-running
AI/notification tasks without blocking the API.
"""

import time


def run():
    while True:
        # Replace with an SQS receive_message loop for the AWS deployment.
        time.sleep(5)


if __name__ == "__main__":
    run()

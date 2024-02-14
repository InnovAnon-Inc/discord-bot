FROM python:latest

COPY ./ /project
WORKDIR /project
RUN pip install .
#VOLUME ["/var/teamhack/etc"]
ENTRYPOINT [            \
  "/usr/bin/env",       \
  "python",             \
  "-m",                 \
  "message_tracker_bot" \
]

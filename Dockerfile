FROM python:3.10-alpine

# create non-root user
RUN addgroup -S appgroup && adduser -HS appuser -G appgroup

# create app directory and bundle app source
WORKDIR /usr/src/app
COPY src/ ./

# ignore pip warnings for root user
ENV PIP_ROOT_USER_ACTION=ignore
# suppress pip upgrade notices
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# install app dependencies
RUN pip install --no-cache-dir -r requirements.txt

# run as non-root user
USER appuser

CMD [ "python", "-u", "./pagerduty_autoack.py" ]

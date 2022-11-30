FROM python:3.10
MAINTAINER Yakir

# Set an environment variable
ENV APP /app
ENV EXPOSE_PORT 8080
#ENV PROJECT_ENV prod
ENV PIP_ROOT_USER_ACTION=ignore
ENV APP_USER tomcat
ENV APP_USER_ID 1001


# Create the directory and user
RUN groupadd -g $APP_USER_ID -r $APP_USER && useradd -r -u $APP_USER_ID -g $APP_USER $APP_USER
RUN mkdir $APP && chown $APP_USER.$APP_USER $APP
WORKDIR $APP

# Copy the requirements file in order to install
# Python dependencies
COPY --chown=$APP_USER:$APP_USER . .
COPY --chown=$APP_USER:$APP_USER APP-META/entrypoint.sh /bin/entrypoint.sh
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose the port uWSGI will listen on
EXPOSE $EXPOSE_PORT

# We copy the rest of the codebase into the image


# Finally, we run uWSGI with the ini file
USER $APP_USER
ENTRYPOINT ["/bin/entrypoint.sh"]
CMD ["runserver"]
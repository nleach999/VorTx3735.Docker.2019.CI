FROM busybox:1.30 as file_copy


# Use --build-arg FRC_TOOLS_VERSION=YYYY.M.m as part of the build to modify the build version
ARG FRC_TOOLS_VERSION=2019.3.2
ARG FRC_TOOLS_FILENAME=WPILib_Linux-$FRC_TOOLS_VERSION.tar.gz

# Use --build-arg FRC_TOOLS_URI_BASE={path} to perform actions like copying the file from a local
# copy of the tools file.  If not, each build will download the 1GB+ tools archive.
ARG FRC_TOOLS_URI_BASE=https://github.com/wpilibsuite/allwpilib/releases/download/v$FRC_TOOLS_VERSION

ARG FRC_TOOLS=$FRC_TOOLS_URI_BASE/$FRC_TOOLS_FILENAME

# Extract the tools tarball if installed locally or download it from GitHub
ADD $FRC_TOOLS /root/frc2019/

# Expand the tarball if downloaded from GitHub
RUN if [ -e /root/frc2019/$FRC_TOOLS_FILENAME ]; then tar -xf /root/frc2019/$FRC_TOOLS_FILENAME -C /root/frc2019; rm -f /root/frc2019/$FRC_TOOLS_FILENAME; fi

FROM python:3-slim

COPY --from=file_copy /root/frc2019 /root/frc2019

ENV JAVA_HOME=/root/frc2019/jdk

# Prepare gradle in the FRC toolkit
RUN cd /root/frc2019/utility/resources/app/resources/gradle/shared \
&& chmod +x gradlew \
&& ./gradlew \
&& chmod -x gradlew

# Update the FRC tools.
RUN cd /root/frc2019/tools \
&& python3 ToolsUpdater.py

# Update pip just because
RUN pip install --upgrade pip \
&& pip install requests pytz

# Install the custom scripts
COPY log_to_slack.py /sbin/log_to_slack
COPY build_frc_targets.sh /sbin/build_frc_targets

RUN chmod +x /sbin/log_to_slack \
&& chmod +x /sbin/build_frc_targets




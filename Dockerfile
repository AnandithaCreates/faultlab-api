FROM python:3.11

# Keep the container layout simple and predictable for CI and local use.
WORKDIR /app

# Copy the full repository because tests import from the src package.
COPY . /app

# Install runtime and test dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Validate the repository during image build so broken commits fail early.
RUN pytest

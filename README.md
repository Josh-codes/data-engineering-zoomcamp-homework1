# Data-engineering-zoomcamp-homework1

## Question 1. Understanding Docker images

Run docker with the `python:3.13` image. Use an entrypoint `bash` to interact with the container.

What's the version of `pip` in the image?

ANS: 25.3

--> To run docker with python:3.13 image used this shell command
```bash
docker run -it --rm --entrypoint bash python:3.13
```

Once inside write: 
```bash
pip --version
```

## Question 2. Understanding Docker networking and docker-compose

Given the following `docker-compose.yaml`, what is the `hostname` and `port` that pgadmin should use to connect to the postgres database?

ANS: db:5432

## Question 3. Counting short trips

For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a `trip_distance` of less than or equal to 1 mile?

ANS: 8007

```sql
SQL Command: SELECT COUNT(*) AS short_trips
FROM green_taxi_data
WHERE lpep_pickup_datetime >= '2025-11-01'
AND lpep_pickup_datetime < '2025-12-01'
AND trip_distance <= 1;
```

## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance? Only consider trips with `trip_distance` less than 100 miles (to exclude data errors).

Use the pick up time for your calculations.

ANS: 2025-11-14

```sql
SELECT DATE(lpep_pickup_datetime) AS pickup_day,
       MAX(trip_distance) AS max_trip_distance
FROM green_taxi_data
WHERE trip_distance < 100
  AND lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
GROUP BY pickup_day
ORDER BY max_trip_distance DESC
LIMIT 1;
```

## Question 5. Biggest pickup zone

Which was the pickup zone with the largest `total_amount` (sum of all trips) on November 18th, 2025?

ANS: East Harlem North

```sql
SELECT z."Zone" AS pickup_zone,
       SUM(t.total_amount) AS total_revenue
FROM green_taxi_data t
JOIN taxi_zone z
  ON t."PULocationID" = z."LocationID"
WHERE DATE(t.lpep_pickup_datetime) = '2025-11-18'
GROUP BY pickup_zone
ORDER BY total_revenue DESC
LIMIT 1;
```

## Question 6. Largest tip

For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

Note: it's `tip` , not `trip`. We need the name of the zone, not the ID.

ANS: Yorkville West

```sql
SELECT dz."Zone" AS dropoff_zone,
       MAX(t.tip_amount) AS max_tip
FROM green_taxi_data t
JOIN taxi_zone pz
  ON t."PULocationID" = pz."LocationID"
JOIN taxi_zone dz
  ON t."DOLocationID" = dz."LocationID"
WHERE pz."Zone" = 'East Harlem North'
  AND t.lpep_pickup_datetime >= '2025-11-01'
  AND t.lpep_pickup_datetime < '2025-12-01'
GROUP BY dropoff_zone
ORDER BY max_tip DESC
LIMIT 1;
```

## Question 7. Terraform Workflow

Which of the following sequences, respectively, describes the workflow for:
1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

ANS: terraform init, terraform apply -auto-approve, terraform destroy


## Free course by @DataTalksClub: https://github.com/DataTalksClub/data-engineering-zoomcamp/

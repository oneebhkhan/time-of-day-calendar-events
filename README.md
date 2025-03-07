# time-of-day-calendar-events

A python script that can generate a series of events tied to the time of day – particularly for use cases where the events correspond to the position of the sun. Some examples include:
- Suhoor and Iftar times during Ramadan
- Prayer times
- Sunrise and sunset times

## How to use
1. Clone the repository locally:
   ```bash
   git clone git@github.com:oneebhkhan/time-of-day-calendar-events.git
   ```
2. Install poetry using brew:
   
   ```bash
   pip3 install poetry==1.8.4
   ```
3. Install the required packages using Poetry:
   
   ```bash
   poetry install
   ```
4. Run the following command  
    ```bash
    poetry run python main.py \
    --start_date <DD-MM-YYYY> \
    --num_days <NUMBER_OF_DAYS> \
    --duration <DURATION_OF_EVENT> \
    --city <CITY_NAME> \
    --fiqh <FIQH> \
    --adjustment <ADJUSTMENT>
    ```
Explaining the arguments:
- `--start_date`: The start date of the events in the format `DD-MM-YYYY`
- `--num_days`: The number of days for which events are to be generated
- `--duration`: The duration of the event in minutes
- `--city`: The city for which events are to be generated
- `--fiqh`: The fiqh to be used for generating events. Can be either `Hanafi` or `Jafari`. (default is `Hanafi`)
- `--adjustment`: The adjustment to be made to the events in minutes (default is 0)

Example:
```bash
   poetry run python main.py \
    --start_date 02-03-2025 \
    --num_days 30 \
    --duration 30 \
    --city Lahore
```

> **Note:** 
> If the `--fiqh` argument is set to `Jafari`, events will be adjusted by 10 minutes by default to account for the difference in Suhoor/Iftar times between the Hanafi and Jafari fiqhs.
> However, if a different preferred adjustment is required, e.g. 12 or 15 minutes, this can be set using the `--adjustment` argument.
> If the `--fiqh` argument is set to `Hanafi`, the `--adjustment` argument will have no effect.

### Known issues/limitations:
- The script currently only supports generating Suhoor and Iftar times for Ramadan.
- The Geocode.xyz API is throttled, if an Exception is raised, simply try again in a few seconds (or minutes).
- The Geocody.xyz API fetches the lat / long coordinates of the city. However it may end up fetching the coordinates of a different/wrong city, e.g. when the city name is `Islamabad` it provides coordinates of `Chittagong, Bangladesh`

### Todo:
Extend to cover more use cases:
- Sunrise / Sunset times
- Prayer times

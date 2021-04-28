## Auxiliary scripts
The auxiliary scripts were created to perform the pre-processing of the collected data before carrying out the analyzes

## What each script does

### auto_scaling_groups.py
 - Count how many machines are in each auto scaling group in each
   timestamp. 
  - You must pass the files in the `/asg` folder as parameters
   to this script.

### as_activity_log.py
- Add the second information to the csv: who was the actor of the action (User or automatic) and if it was a machine addition or removal (Scale-out or Scale-in).
- You must pass the files in the `/asg-events` folder as parameters to this script.

### utilization.py
- Removes collections with repetition of the timestamp together with the instanceId and metricName.
- You must pass the files in the `/teste-1` folder as parameters to this script.

### load_balancer.py
- Removes collections with repetition of the timestamp together with the LoadBalancer
- You must pass the files in the `/teste-2` and `/teste-3` folder as parameters to this script.

### concatenate_files_by_day.py
- Concatenates the treated files in just one per day.
- You must pass the files treated by the scripts described above as parameters for this script.

## How to run?

### auto_scaling_groups.py
| Argument | Description |
-----|-----
| folder | Folder where the files are |
| output_folder | Folder where the treated files will be saved |

```
python3 auto_scaling_groups.py --folder=/home/gabriela/data/asg/01-03_to_08-03_2/ --output_folder=/home/gabriela/data/result/asg/01-03_to_08-03_2/
```
### as_activity_log.py
| Argument | Description |
-----|-----
| folder | Folder where the files are |
| output_folder | Folder where the treated files will be saved |

```
python3 as_activity_log.py --folder=/home/gabriela/data/asg-events/01-03_to_08-03_2/ --output_folder=/home/gabriela/data/result/asg-events/01-03_to_08-03_2/
```
### load_balancer.py
| Argument | Description |
-----|-----
| folder | Folder where the files are |
| output_folder | Folder where the treated files will be saved |

```
python3 load_balancer.py --folder=/home/gabriela/teste-2/01-03_to_08-03_2/ --output_folder=/home/gabriela/data/result/teste-2/01-03_to_08-03_2/
```
### utilization.py
| Argument | Description |
-----|-----
| folder | Folder where the files are |
| output_folder | Folder where the treated files will be saved |

```
python3 utilization.py --folder=/home/gabriela/teste-1/01-03_to_08-03_2/ --output_folder=/home/gabriela/data/result/teste-1/01-03_to_08-03_2/
```

### concatenate_files_by_day.py
| Argument | Description |
-----|-----
| folder | Folder where the files are |
| output_folder | Folder where the treated files will be saved |
| timestamp_column_name | column with the collection timestamp (timestamp, StartTime or EndTime) |
| frequency | Frequency in minutes that collections are performed (15 or 60) |
```
python3 concatenate_files_by_day.py --folder=/home/gabriela/result/asg/01-03_to_08-03_2/ --output_folder=/home/gabriela/result/asg/day/01-03_to_08-03_2/ --timestamp_column_name="timestamp" --frequency=15
```
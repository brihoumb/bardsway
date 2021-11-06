# JSON Writer module for Bard's Way #
>
> Write JSON from Bard's Way information.
>

## Summary: ##
- Usage
- JSON Template
- Functions

## Usage: ##
Start the `init_instrument_json` method at the beginning of your function.  
Then use `append_note_json` method for each note you want to add in your JSON partition.  
Finally use `final_write_json` method to write the JSON file partition.  

```python
init_instrument_json(instrument_name = str(), version = str(), bpm = int(), duration = str())
append_note_json(note = str(), pitch = int(), time_end = int(), time_start = int())
final_write_json(path_to_write = str())
```

## JSON Template: ##
```JSON
{
	"version": "X.X.X",
	"instrument": "",
	"BPM": 0,
	"duration": "XX:XX:XX.XXX",
	"notes": [
		{
			"note": "",
			"pitch": 0,
			"time_end": 0,
			"time_start": 0
		}
	]
}
```
##  Functions: ##

```python
init_instrument_json(instrument_name = str(), version = str(), bpm = int(), duration = str())
```
>
> Initiate the JSON to be written.
>

#### Parameters: ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**instrument_name** Name of the instrument.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**version** Bard's Way version.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**duration** Music duration in HH:mm:ss.fff.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**BPM** Beat per minute of the music.  

---

```python
append_note_json(note = str(), pitch = int(), time_end = int(), time_start = int())
```

>
> Append the note to the notes array.
>

#### Parameters: ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**note** Name of the note in [Romance format](https://en.wikipedia.org/wiki/Solf%C3%A8ge#Fixed_do_solf%C3%A8ge).  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**pitch** Musical pitch of the note.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**time_end** Time where the note is released.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**time_start** Time where the note is pressed.  

---

```python
final_write_json(path_to_write = str())
```

>
> Write the partition in the JSON file and close the editing.
>

#### Parameters: ####

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**path_to_write** Path were the JSON file need to be written.

# Data Formating module for Bard's Way #
>
> Formate all the data from audio analyser in a JSON.
>

## Summary: ##
- Usage
- Functions
- Library Used

## Usage: ##
Class `DataFormatig` with method to calculate the short fourier transform of the given audio sample.

```python
__init__(self, length, name)
print(self, filename)
add_data(self, name, data)
```
##  Functions: ##

```python
__init__(self, length, name)
```
>
> Initiate the JSON with the length and the name of the file.
>

#### Parameters: ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**self** self.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**length** Length of the file.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**name** Name of the file.  

---

```python
print(self, filename=str())
```
>
> Create a file with the formated data inside of a JSON.
>

#### Parameters: ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**self** self.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**filenme** Name of the json output.  

---

```python
add_data(self, name=str(), data=dict())
```
>
> Insert value in the JSON.
>

#### Parameters: ####
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**self** self.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**name** Key to create.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**data** Value to assign to the key.  

##  Library Used: ##

We use `json` to dump JSON in file.

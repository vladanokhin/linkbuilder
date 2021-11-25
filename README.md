# Link Builder for Hugo Sites


### Installation

1. Create virtual env 
```bash
    python3 -m venv .env/
```

2. Activate virtual env (for linux)
```bash
    source .env/bin/activate
```
3. Install requiments
```bash
    pip3 install -r requiments/requiments.txt
```

### Configuration

Need to edit the file **config.py** before using the script. Set the correct values of **NUMBER_LINK_TO_ADD** and **PHRASES_FOR_LINKS**

1.*NUMBER_LINK_TO_ADD*: number of links to add to the original page you can set it as a number:
```python        
NUMBER_LINK_TO_ADD = 5
```
Or as a range, then will be added from 3 to 7 links, the values are chosen randomly:
```python
NUMBER_LINK_TO_ADD = (3,7)
```

2. *PHRASES_FOR_LINKS*: phrases that will be randomly inserted before the links

```python
PHRASES_FOR_LINKS = [
    'Read More',
    'Also',
    'More',
    'More information',
    'Additional information'
]
```  

### Preview

Example of inserted links in a post

```md
You cаn order a thesis, a dissertation, and a case study in any discipline. You can order any type of assignment yоu need. We can also help you with math homework if you need it.

## Additional information:
[How To Begin An Argumentative Essay](https://50essaysonline.info/essay-topics/how-to-begin-an-argumentative-essay/)

[Good Research Essay Topics For College](https://50essaysonline.com/good-research-essay-topics-for-college/)


## Why Should You Choose Our Cheap Essay Writing Service?

You may have many reasons why yоu should hire our cheap essay writing service. If you are looking for the best essay writing service, then you should look no further. We are the best essay writing service because we offer a variety of services at a cheap price.
```


### Basic usage of the script

Run the file **run.py** with the flag **-l** (required). Where **-l** flag is the path to the file with the list of sites for which you want to add relevant

```bash
    python3 run.py -l path/to/list.txt
```

 An example of a file with a list of sites:

    2dayessay.com
    48hrcopywriting.com
    50essaysonline.com
    50essaysonline.info


After successful execution of the script the table with the result will be printed:

    | Domain              |   Added Relevant Links |
    |---------------------|------------------------|
    | 2dayessay.com       |                     18 |
    | 48hrcopywriting.com |                      6 |
    | 50essaysonline.com  |                      1 |
    | 50essaysonline.info |                      3 |
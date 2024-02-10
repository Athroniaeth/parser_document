# Architecture
## Note
if you want the same schema of application, use WSL (Linux) and install tree and use it with `directory` mode.
``` commandline
sudo apt install tree
tree -d . > tree_directory.txt
```

## Project folder
```toml
.
│ # Folder contains client data
├── data 
│
│ # Folder contains technical documentation
├── docs 
│
│ # Folder contains reports on accuracy of algorithms
├── reports 
│
│ # Folder contains technical scripts for CI/CD
├── scripts 
│
│ # Folder contains source code
├── src 
│
│ # Folder contains tests
└── tests

6 directories
```


## Data folder
```python
├── data
│   │ # Folder contains client documents
│   ├── 01_raw_documents
│   │
│   │ # Folder contains images extract from document
│   ├── 02_raw_images
│   │
│   │ # Folder contains preprocess images (dim, shape, norm)
│   ├── 03_preprocess_images
│   │
│   │ # Folder contains client documents (noise, bin, contrast)
│   ├── 04_clean_images
│   │
│   │ # Folder contains bbox from OCR 
│   ├── 05_extracted_bbox_images
│   │
│   │ # Folder contains client documents
│   └── 06_detected_bbox_images
...

7 directories
```

## Source folder

```diagram
graph TD
    A[Hard] -->|Text| B(Round)
    B --> C{Decision}
    C -->|One| D[Result 1]
    C -->|Two| E[Result 2]
```
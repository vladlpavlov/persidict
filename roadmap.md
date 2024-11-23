# Development Roadmap for PersiDict project

* Add compatibility tests/support for more Python libraries, 
starting with those popular in the DS/ML/AI community 
(TensorFlow, PyTorch, SKLearn, Polars, LightGBM, etc.).
* Add support for more storage backends, starting with Azure and GCP.
* Add max_scan_size attribute to base PersiDict class to 
limit the number of rows scanned by PersiDict methods.
* Add backend-specific optimizations for time-consuming operations.
## Custom Regression Model

### `regression_model_cloth_v01.py`
This Python script trains a custom regressive model to implement character cloth simulation into a Houdini-internal Onnx inference to obtain real-time cloth sim performance. Trained on generic motion capture animation data on a generic procedurally-built character mesh as the inputs and the same animation data with Houdini cloth simulations to deform the generic character mesh as the output targets. The result is a 30 minute training time to obtain decent real-time deformation results.
[View the script here](https://github.com/JMTechArt/Pipeline-Examples/blob/main/Machine_Learning/Custom_Regression_Model/regression_model_cloth_v01.py)

### Results on the left, original input on right
![cloth_regression](../IMG/ClothRegression.gif)
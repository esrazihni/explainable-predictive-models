# Opening the Black Box of Artificial Intelligence for Clinical Decision Support: A Study Predicting Stroke Outcome 

This repository contains the implementation and evaluation of linear (GLM, Lasso and Elastic Net) and non-linear (Tree Boosting and Multilayer Perceptron) models for predicting stroke outcome in acute-ischemic patients; as well as the implementation of explainability methods to determine clinical predictors (features) importance for outcome prediction. 

## Publication

https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0231166


## Data
314 patients with acute ischemic stroke from the 1000plus study were included. Currently the clinical data cannot be made publicly accessible due to data protection.

__Input:__ Clinical predictors (features) (7)

    AD_NIH: NIHSS at admission
    AT_LY: thrombolysis
    CH: history of cardiac diseases
    DG_SEX: gender
    RF_DM: diabetes
    RF_HC: hypercholesterolemia
    DG_AG: age

__Output:__ 3 months post-stroke mRS score (good (mrs<=2) : 226 patients , bad (mrs>=3) : 88 patients)

__Exclusion Criteria:__

* Patients with no mRS information were excluded.
* Patients with infratentorial stroke and no visible DWI lesions were excluded.
* Clinical predictors with more than 5% missing values were excluded.
* Categorical clinical predictors with a yes/no ratio larger than 1/4 were excluded, in order to prevent category imbalance.                               

The table below presents the clinical characteristics of the 1000plus dataset.

| Clinical Information             | Value       | Clinical Information           | Value    | 
|----------------------------------|-------------|--------------------------------|----------|
| Median age (IQR)                 | 72.0 (15.0) | Cardiac history (yes/ no)      | 84/ 230  | 
| Median Initial NIHSS (IQR)       | 3 (5)       | Diabetes (yes/ no)             | 79/ 235  | 
| Thrombolysis (yes/ no)           | 74/ 240     | Hypercholesterolemia (yes/ no) | 182/ 132 |  
| Sex (Females/ males              | 196/ 118    | 								                |          |

The figures below show the distribution of continuous and categorical predictors in the 1000plus dataset.

<p align="center">
<img src="images/1kplus_hist_of_numerical_data.png" alt="fig1.1" width="500"/>
<img src="images/1kplus_hist_of_categorical_data.png" alt="fig1.1" width="500"/>
</p>

## Methods:

### Data Preprocessing
* The continuous predictors were centered using zero-mean unit-variance normalization.
* Missing values were imputed using mean imputation
* Both pre-processing steps were applied based on the training set after the data was split into training and test sets.

### Multicollinearity analysis
The Variance Inflation Factor (VIF) was calculated for each of the clinical predictors to measure multicollinearity. The VIF analysis demonstrated negligible multicollinearity with VIFs < 1.91. The calculated VIF values for each predictor is given in the table below.

|  Predictor Name | AD_NIH  | CH   | DG_SEX | RF_DM | RF_HC | DG_AG | AT_LY | 
|-----------------|---------|------|--------|-------|-------|-------|-------|
|  VIF            | 1.28    | 1.33 | 1.91   | 1.36  | 1.74  | 1.15  | 1.50  |

### Cross-validation Design
* The data was split into training and test sets with a 4/1 ratio. Same training and test sets were used in all models to achieve comparable results. 
* The models were tuned, i.e best hyperparameters were selected, using 10-folds cross-validation with gridsearch. Same folds were used for all models to achieve comparable results.
* In order to account for data variability the above process was repeated 50 times; resulting in 50 splits tuned separately for each model.

### Subsampling
To target class imbalance, the training set was randomly sub-sampled to yield equal number of label classes, i.e equal number of patients with good and bad outcome.

### Linear predictive models: GLM, Lasso, Elastic Nets
1. GLM (General Linear Model): A logistic regression model with no regularization term was implemented using sklearn's LogisticRegression class. 
            
2. Lasso: A logistic regression model with L1 regularization was implemented using sklearn's LogisticRegression class. The strength of the regularization was adjusted using a tuning hyperparameter alpha. The best value of alpha was chosen during model tuning. 

3. Elactic Nets:  A logistic regression model with both L1 and L2 regularization was implemented using sklearn's SGDClassifier class. The strength of the different regularizations was adjusted using tuning hyperparameters alpha and gamma. The best values of alpha and gamma were chosen during model tuning.

### Non-linear predictive model: Tree Boosting
A tree-boosting model is implemented using the [Catboost](https://tech.yandex.com/catboost/) package for Python. The parameter for optimal tree count was automatically tuned by setting the overfitting detection parameters of the package. The best values of the L2 regularization term, tree depth, learning rate, leaf estimation iterations and bagging temperature were chosen during model tuning.

### Non-linear predictive model: Multilayer Perceptron (MLP)
An MLP model consisting of a single hidden layer was implemented using Keras running on Tensorflow backend. Early stopping was introduced during training in order to prevent overfitting. The best values of the L2 regularization term, dropout rate, batch size, learning rate and number of neurons in the hidden layer were chosen during model tuning.

### Final performance assessment
For each model:
* Training and test performances are evaluated on the respective training and test sets of each split using Area Under the Receiver Operating Characteristics curve (AUC). 
* The final performance is the median and iqr of the training and test AUC scores computed over 50 splits.

### Clinical parameters rating
Three different explainability methods tailored to the different ML algorithms were used to calculate importance values for the clinical predictors used in the scope of this project. 

1. GLM, Lasso and Elastic Net: Weights assigned to input features (predictors) in the trained GLM, Lasso and Elasticnet models were used as feature impoartance values.
2. Tree Boosting (Catboost): Shapley values were used for systematically rating the importance (gain) of each of the input features (predictors) in the trained Catboost model. Shapley values were obtained using the [SHAP](https://github.com/slundberg/shap) package for Python.
3. MLP: A gradient based algorithm called deep Taylor decomposition was used to find salient features in the trained MLP model. The gradients were obtained using the [INNvestigate](https://github.com/albermax/innvestigate) package for Python.

* The absolute values of the calculated feature importance scores were scaled to unit norm (i.e normalized) in order to provide comparable feature rating across models. 
* The final importance value assigned to each feature is the mean and standard deviation of their normalized scores over 50 splits.

## Results:

### Performance Results

The table below presents the performance results of the different models calculated as AUC scores over 50 splits.

| Model      | Value  | AUC (training) | AUC (test) | 
|------------|--------|----------------|------------|
| GLM        | median | 0.83           | 0.82       |
|            | iqr    | 0.02           | 0.09       |
| Lasso      | median | 0.83           | 0.82       | 
|            | iqr    | 0.03           | 0.07       | 
| ElasticNet | median | 0.82           | 0.79       | 
|            | iqr    | 0.04           | 0.09       | 
| Catboost   | median | 0.85           | 0.81       | 
|            | iqr    | 0.03           | 0.07       | 
| MLP        | median | 0.82           | 0.81       | 
|            | iqr    | 0.03           | 0.07       | 

The figure below illustrates the performance of the different models evaluated on the test (blue) and training (orange) sets. The markers show showing the median AUC over 50 splits and the error bars represent  interquartile range (IQR).

<p align="center">
<img src="images/AUC_scores_random_subsampling.png" alt="fig2" width="500"/>
</p>

### Clinical Predictors Importance Ratings

The figure below illustrates the features rating derived from the model-tailored interpretability methods. The bar heights represent means and error bars represent standard deviation over 50 splits.

![](images/clinical_predictor_ratings_all_models_random_subsampling.png)

## Manual
Manual to this framework can be found [here](manual.md).

## License
This project is licensed under the [MIT license](LICENSE).




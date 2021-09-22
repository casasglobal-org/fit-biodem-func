# fit-biodem-func

Application to fit the rate of development on temperature as part of a set of bio-demographic functions for modeling basic biological processes in any organism using physiologically based demographic models (PBDMs, see <http://bit.ly/Gutierrez-1996> and <https://doi.org/10.1603/EN12018>). The basic idea would be to develop functionality similar to the `devRate` R package (see <https://cran.r-project.org/package=devRate>) using the `lmfit` Python package (see <https://lmfit.github.io/lmfit-py/>).

Mind map for `bio-dem_fit` app:![mind map for `bio-dem_fit` app](https://user-images.githubusercontent.com/40238010/113409093-dad74400-93b0-11eb-92b5-2d1df2e6dea2.png)

## Running the app

```bash
git clone git@github.com:luisponti/fit-biodem-func.git
cd fit-biodem-func
poetry install
export FLASK_ENV=development
export FLASK_APP=fit_biodem_func/views.py
mkdir uploads
cp .env-template .env
# set the required environment variables to work with a DB and an AWS S3 bucket
poetry run flask run
```

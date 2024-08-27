# This is used to make sure the user enters a valid ZIP code.
# The pyzipcode library needs to be used for the ZIP code validation code to work.
zdb = ZipCodeDatabase()


# This is the form for the Weather Forecast app.
class WeatherForm(forms.Form):
    # Define a CharField for the ZIP code with a maximum length of 5 characters.
    zip_code = forms.CharField(label="ZIP Code:", max_length=5)

    # Define a custom clean method for the zip_code field.
    def clean_zip_code(self):
        # Retrieve the zip_code from the cleaned_data dictionary.
        zip_code = self.cleaned_data["zip_code"]
        try:
            # Attempt to access the zip_code in a ZIP code database (zdb).
            # This line will raise an exception if the zip code is not found in the database.
            zdb[zip_code]
        except (KeyError, IndexError):
            raise ValidationError(
                "You've made an invalid submission. Please enter a valid ZIP code."
            )
        # If no exception is raised, return the validated zip_code.
        return zip_code

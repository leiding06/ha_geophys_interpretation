def toggle_checkboxes( checkbox, other_checkbox):
        """
        Exclusive the checkbox and other_checkbox, only one will be checked
       
        """
        if checkbox.isChecked():
            other_checkbox.setChecked(False)  # Uncheck the other checkbox
        else:
            checkbox.setChecked(False)  # Allow unchecking
class Error:
    """
    Error class representing an issue with lexing, parsing, or interpretation
    """
    def __init__(self, type_, details, fn=None, ln=None):
        self.type = type_
        self.details = details
        self.fn = fn
        self.ln = ln

    def __str__(self):
        result = f"{self.type}: {self.details}\n"
        if self.fn is not None and self.ln is not None:
            result += f"File {self.fn}, line {self.ln}"
        return result

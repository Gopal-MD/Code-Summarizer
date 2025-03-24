# Create the data directory if it doesn't exist
mkdir -p data

# Create an example Python file with some content
echo '
def calculate_sum(a: int, b: int) -> int:
    """
    Calculate the sum of two integers.
    
    Args:
        a: First integer
        b: Second integer
        
    Returns:
        The sum of a and b
    """
    return a + b
' > data/example.py
import subprocess

def execute_curl_command():
    # Execute the curl command
    curl_process = subprocess.Popen(['curl', 'https://ulx2rea77nvxmr5hr3opqfx7yi0waayl.lambda-url.ap-northeast-2.on.aws/'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Capture the output and error (if any)
    output, error = curl_process.communicate()
    
    # Decode the output and error to strings
    output_str = output.decode('utf-8')
    error_str = error.decode('utf-8')
    
    return output_str, error_str

# Execute the curl command and capture the output
output, error = execute_curl_command()

# Print the output and error
print('Output:')
print(output)

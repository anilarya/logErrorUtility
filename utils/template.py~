 
def email_content_for_error_count():    
    email_body = """
        <html>
        <head>
          <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
          <title>html title</title>
          <h4 align= "center"> Summary :Daily Status Report</h4>
        </head>
        <body>
            <h4 align="center"> Start Timestamp : %s] - End Timestamp : %s] </h4> 
            <table align= "center" border= "1px solid">
                <thead >
                  <tr bgcolor="silver">
                    <th>Project_Name</th>
                    <th>Total Count</th>
                    <th>4xx Error Count</th>
                    <th>5xx Error Count</th> 
                    <th>2xx Count</th> 
                  </tr>
                </thead>
                <tbody>
                  <tr border = 1px black>
                    <td>Project_name</td>
                    <th>%d</th>
                    <td>%d </td>
                    <td>%d</td>
                    <td>%d</td>  
                  </tr>
                </tbody> 
              </table>  
              <table>
        </body>
        </html>
        """

    return email_body


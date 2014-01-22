 
def email_content_for_error_count():    
    email_body = """
         <html>
          <head>
          <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>html title</title>
            <h4 align= "center"> Summary :Daily Status Report</h4>
          </head>
          <body>
          <h4 align="center"> [Date  : %s] </h4> 
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
                  <td>Lithium</td>
                  <th>%d</th>
                  <td>%d </td>
                  <td>%d</td>
                  <td>%d</td>  
                </tr>
              </tbody> 
            </table>
            <br> 
            <br>
            <div align="center"> <strong>Error PI-CHART</strong><br>
            <img src="https://chart.googleapis.com/chart?chs=350x200&chd=t:%d,%d,%d&cht=p&chl= 5xx-Count|4xx-Count|2xx-Count&chco=FF0000|FFA500|00FF00 "/>
             </div><br>
             <strong>PFA 5xx log errors :</strong>  
          </body>
        </html>
        """
        
    return email_body


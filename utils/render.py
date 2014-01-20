import template

def get_email_html_body(start_timestamp, count): 
    a =  getattr(template,'email_content_for_error_count' ) 
    email_body = a()%(start_timestamp, count['total']['total_Count'], count["4xx"][ "4xx_Counts"],\
              count["5xx"][ "5xx_Counts"], count["2xx"][ "2xx_Counts"],count["5xx"][ "5xx_Counts"],\
              count["4xx"][ "4xx_Counts"], count["2xx"][ "2xx_Counts"])
    return email_body
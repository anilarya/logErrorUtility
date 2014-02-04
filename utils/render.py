import template
import settings


def get_email_html_body(start_timestamp, count):
    a =  getattr(template,'email_content_for_error_count' ) 
    _4xx = count["4xx"][ "4xx_Counts"]
    _5xx = count["5xx"][ "5xx_Counts"]
    _2xx = count["2xx"][ "2xx_Counts"]
    sum = _4xx +  _5xx + _2xx
    if sum !=0 : 
        _4xx_per = ( _4xx / float(sum))*100
        _5xx_per = ( _5xx / float(sum))*100
        _2xx_per =  ( _2xx / float(sum))*100 
    
    email_body = a()%(start_timestamp, settings.project, count['total']['total_Count'], count["4xx"][ "4xx_Counts"],\
              count["5xx"][ "5xx_Counts"], count["2xx"][ "2xx_Counts"],_5xx_per , _4xx_per , _2xx_per)
    return email_body
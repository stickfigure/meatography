This is software for the world's first internet-enabled salumi curing cabinet.

Seriously.

When it is finally live, you can see it at http://www.meatography.com.

We hope to provide enough instructions that you can build one of these on your own.  There are two components:

  1. The Cabinet
    * The hardware of the curing cabinet
    * 1wire sensor for temp and humidity (and possibly salumi weight)
    * Controls for 110v appliances; humidifier, dehumidifier, refrigeration, heating
    * Linux-based plug computer controller which communicates with the server
  1. The Server
    * Runs on Google App Engine (Python)
    * Provides status of cabinet, historical graphs
    * Sets temp & humidity goals for cabinet
    * Emails alerts when cabinet is outside spec or stops reporting
    * Includes the Moe wiki, but this can be removed
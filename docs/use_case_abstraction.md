# Use cases

## Push media files to Media Consumption Area

Components:

* Media Source
* Media Collector
* Media Consumption Area

Description:

* The `Media Source` is able to send media files to the `Media Collector` that stores them to the `Media Consumption Area`.
    * The `Media Source` uses a "`Send only`" pattern. 
        * New files in the `Media Source` are sent to the `Media Collector`. 
        * Once the transmission is confirmed the `Media Source` will never again try to transmit this file. 
        * Altered files are treated as new files not as updates.
        * Deletions in the `Media Source` are not populated to the `Media Collector`.
    * The `Media Collector` uses a "`Receive only`" pattern.
        * New files from `Media Source` are stored to the `Media Consumption Area`.
        * Updates from `Media Source` to existing files in the `Media Consumption Area` are ignored.
        * Deletions from `Media Source` to existing files in the `Media Consumption Area` are ignored.
        * Changes to files in the `Media Consumption Area` are not populated to the `Media Source`.

## Pull media files to Media Consumption Area

Components:

* Media Source
* Media Collector
* Media Consumption Area

Description:

TBD

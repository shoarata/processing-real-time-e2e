* To download jars necessary for running flink job locally
    ```bash
    mvn clean package dependency:copy-dependencies -DoutputDirectory=jars/
    # then delete created target directory
    rm -r target/
    ```
* Ip data taken from: https://lite.ip2location.com/database/db1-ip-country

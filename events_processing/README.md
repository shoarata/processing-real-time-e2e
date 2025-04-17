```bash
cd events_processing/
# to download and copy jars needed to jar directory run 
mvn clean package dependency:copy-dependencies -DoutputDirectory=jars/
# then delete created target directory
rm -r target/
```

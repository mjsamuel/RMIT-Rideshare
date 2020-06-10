# Going to correct directory based on command line arguments
if [[ $1 == "1" ]]
then
  cat config.ini.example >> config.ini
  cd master_pi
fi

if [[ $1 == "2" ]]
then
  cd agent_pi
fi

# Running pytest and exit on error if an error occurred
if ! pytest; then
  exit 1
fi

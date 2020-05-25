
if [[ $1 == "1" ]]
then
  cat config.ini.example >> config.ini
  cd master_pi
  pytest
fi

if [[ $1 == "2" ]]
then
  cd agent_pi
  pytest
fi

import React, {useEffect, useState} from 'react';
import { Stack } from '@mui/system';
import TabButton from '../../buttons/TabButton';
import RecordBookTable from '../../tables/RecordBookTable';
import API from '../../../../api';


export default function RecordBookTabs() {
  const [records, setRecords] = useState([]);
  const [realRecords, setRealRecords] = useState([]);
  const [tab, setTab] = useState(0);
  const [terms, setTerms] = useState([]);

  useEffect(() => {
    const getUserData = async () => {
      const result = await API.get(`/user/me`, {headers: {Authorization: `Bearer ${localStorage.getItem('access_token')}`}});
      setRecords(result.data.records);
      for (let i = 0; i < result.data.records.length; i++) {
        if (!terms.includes(result.data.records[i].term)) {
          terms.push(result.data.records[i].term);
        }
      }
      setTab(result.data.records[terms.length - 1].term);
      setRealRecords(result.data.records.filter((record) => record.term === result.data.records[terms.length - 1].term));
    };
    getUserData();
  }, [terms])

  const handleClick = (event) => {
    const index = parseInt(event.target.innerText.split(' ')[0]);
    setTab(index);
    const filteredRecords = records.filter(x => x.term === index);
    setRealRecords(filteredRecords);
  };

  return (
    <Stack sx={{ gap: '32px', m: '0 auto' }}>
      <Stack direction='row' sx={{ gap: '32px', m: '0 auto' }}>
        {terms.map((term) => (
          <TabButton key={term} onClick={handleClick} active={tab === term ? true : false}>{term} семестр</TabButton>
        ))}
      </Stack>
      <RecordBookTable rows={realRecords} term={tab}/>
    </Stack>
  );
}

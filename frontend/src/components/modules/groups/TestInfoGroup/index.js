import {
  FormControl,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  TextField,
} from '@mui/material';
import { Stack } from '@mui/system';
import React, { useEffect, useState } from 'react';
import AppButton from '../../../elements/buttons/AppButton';
import API from '../../../../api';


export default function TestInfoGroup() {
  const [student, setStudent] = useState('');
  const [subject, setSubject] = useState('');
  const [type, setType] = useState('');
  const [mark, setMark] = useState('');
  const [semester, setSemester] = useState('');
  const [date, setDate] = useState('');
  const [year, setYear] = useState('');
  const [students, setStudents] = React.useState([]);
  const [years, setYears] = React.useState([]);
  const typeItems = [
      <MenuItem value="Отлично">Отлично</MenuItem>,
      <MenuItem value="Хорошо">Хорошо</MenuItem>,
      <MenuItem value="Удовлетворительно">Удовлетворительно</MenuItem>,
  ]
  useEffect(() => {
    const getStudentsData = async () => {
      const result = await API.get(`/student`, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } });
      setStudents(result.data);
    };
    const getYearsData = async () => {
      const result = await API.get(`/year`, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } });
      setYears(result.data);
    };
    getStudentsData();
    getYearsData();
  }, [])

  const handleChangeStudent = e => {
    setStudent(e.target.value);
  };

  const handleChangeSubject = e => {
    setSubject(e.target.value);
  };

  const handleChangeType = e => {
    setMark('');
    setType(e.target.value);
  };

  const handleChangeMark = e => {
    setMark(e.target.value);
  };

  const handleChangeSemester = e => {
    setSemester(e.target.value);
  };

  const handleChangeDate = e => {
    setDate(e.target.value);
  };

  const handleChangeYear = e => {
    setYear(e.target.value);
  };

  const handleSubmit = e => {
    e.preventDefault();
    const createMark = async () => {
      const markData = {
        "name": subject,
        "term": semester,
        "mark": "Отлично",
        "exam_date": date,
        "exam_type": type
      }
      await API.post(`/student/${student}/record?year=${year}`, markData, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } });
    };
    createMark();
    setStudent('');
    setSubject('');
    setType('');
    setMark('');
    setSemester('');
    setDate('');
    setYear('');
  };

  return (
    <Paper
      sx={{
        p: '16px',
        boxShadow: '0px 4px 20px rgba(83, 83, 83, 0.1)',
        borderRadius: '12px',
      }}>
      <form onSubmit={handleSubmit}>
        <Stack sx={{ gap: '32px' }}>
          <Stack
            direction='row'
            sx={{
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '16px',
            }}>
            <FormControl fullWidth>
              <InputLabel>Студент</InputLabel>
              <Select
                id='demo-simple-select'
                value={student}
                label='Студент'
                onChange={handleChangeStudent}>
                {students.map((student, index) => (
                  <MenuItem key={index} value={student.guid}>
                    {student.last_name} {student.first_name} {student.middle_name} {student.group}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              label='Предмет'
              value={subject}
              onChange={handleChangeSubject}
            />
            <FormControl fullWidth>
              <InputLabel>Тип экзамена</InputLabel>
              <Select
                id='demo-simple-select'
                value={type}
                label='Тип экзамена'
                onChange={handleChangeType}>
                <MenuItem value="Зачет">Зачет</MenuItem>
                <MenuItem value="Экзамен">Экзамен</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Оценка</InputLabel>
              <Select
                id='demo-simple-select'
                value={mark}
                label='Оценка'
                onChange={handleChangeMark}>
                {type === "Зачет" ? (
                  <MenuItem value="Зачтено">Зачтено</MenuItem>
                ) : (typeItems)}
              </Select>
            </FormControl>
            <TextField
              label='Семестр'
              value={semester}
              onChange={handleChangeSemester}
            />
            <TextField
              label='Дата экзамена'
              value={date}
              onChange={handleChangeDate}
            />
            <FormControl fullWidth>
              <InputLabel>Год обучения</InputLabel>
              <Select
                id='demo-simple-select'
                value={year}
                label='Год обучения'
                onChange={handleChangeYear}>
                {years.map((year, index) => (
                  <MenuItem key={index} value={year.guid}>
                    {year.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Stack>
          <AppButton type='submit' sx={{ p: '16px' }}>
            Добавить
          </AppButton>
        </Stack>
      </form>
    </Paper>
  );
}

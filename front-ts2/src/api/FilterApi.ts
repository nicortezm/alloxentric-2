import axios from 'axios'

const FilterAPI = axios.create({
    baseURL: 'http://127.0.0.1:9090',
    headers: { 'Content-Type': 'application/json' },
    auth: {
        username: 'usuario1',
        password: 'usuario1'
      }
})


export default FilterAPI;


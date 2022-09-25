
import './App.css';
import BarChart from "./Components/BarChart";
import React, {useState} from "react";
import OutputLabel from "./UI/Output/OutputLabel";
import InputBut from "./UI/Input/InputBut";
import MyButton from "./UI/MyButton/MyButton";
import MyModal from "./UI/MyModal/MyModal";
import LineChart from "./Components/LineChart";
import sampleData from './Data'







function App() {
    const [label,SetLabel] = useState('Popa');
    const [drag,setDrag] = useState(false);
    const [modal, setModal] = useState(false);
    const [data,setData] = useState({
        labels: sampleData.map((data) => data.mount),
        datasets: [{
            label: 'Процент инфлации за месяц',
            data: sampleData.map((data) => data.prechange),
            borderColor: 'blue'
        }]
    })
    function closeModal() {
        setModal(false)
    }
  return (


        <div className="App">
            <MyModal visible={modal} setVisible={setModal}>
                <InputBut drag={drag} setDrag={setDrag} funct={closeModal}>
                </InputBut>
            </MyModal>
            <header>
                <MyButton onClick={() => setModal(true)}>Загрузка датасета</MyButton>
            </header>
            <LineChart CharData={data}/>
        </div>
  );
}

export default App;

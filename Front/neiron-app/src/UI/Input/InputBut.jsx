import React from 'react';
import classes from './InputBut.module.css'
import axios from "axios";
const InputBut = ({drag,setDrag,funct}) => {
    function dragStartHandler(e){
        e.preventDefault()
        setDrag(true)


    }
    function dragLeaveHandler(e){
        e.preventDefault()
        setDrag(false)
    }
    function onDropHandler(e){
        e.preventDefault()
        funct()
        let files = [...e.dataTransfer.files]

        const formData = new FormData()
        formData.append('file', files[0])
        console.log(formData)
        axios.post('http://127.0.0.1:8000/files/', formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            }
        })
            .then(function (response) {
                console.log(response.data);
            });


        setDrag(false)
    }

    return (
        <div>
            {drag
                ? <div
                    onDragStart={e => dragStartHandler(e )}
                    onDragLeave={e => dragLeaveHandler(e )}
                    onDragOver={e => dragStartHandler(e )}
                    onDrop={e => onDropHandler(e )}
                    className={classes.dropArea}>Отпустите файлы, что бы загрузить их</div>
                : <div
                    onDragStart={e => dragStartHandler(e )}
                    onDragLeave={e => dragLeaveHandler(e )}
                    onDragOver={e => dragStartHandler(e )}
                >Перетащите файлы, чтобы загрузить их</div>




            }
        </div>
    );
};

export default InputBut;
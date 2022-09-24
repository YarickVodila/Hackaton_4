import React from 'react';
import classes from './InputBut.module.css'
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
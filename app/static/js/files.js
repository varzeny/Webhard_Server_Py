// files.js

const PAGE = {
    currentPath:[],
    spanPath:null,
    divDir:null,
    divFile:null,
    divDrag:null,
    btnChoice:null,
    btnUpload:null,
    filesToUpload:[],
    init:function(){
        this.spanPath=document.getElementById("span-path");
        this.divDir=document.getElementById("dir");
        this.divFile=document.getElementById("file");
        this.divDrag=document.getElementById("drag");
        this.divDrag.addEventListener("dragover",(e)=>{
            e.preventDefault();
            this.divDrag.classList.add("drag-over");
        });
        this.divDrag.addEventListener("dragleave",()=>{
            this.divDrag.classList.remove("drag-over");
        });
        this.divDrag.addEventListener("drop",(e)=>{
            e.preventDefault();
            this.divDrag.classList.remove("drag-over");

            const droppedFiles = Array.from(e.dataTransfer.files);
            this.filesToUpload = this.filesToUpload.concat(droppedFiles); // 파일을 목록에 추가

            console.log("Files dropped : ", this.filesToUpload);
            if(window.role!="admin"){
                alert(`you are ${window.role}. not admin !`);
            }else{
                alert("일단은 다운로드만 쓰자. 업로드는 나중에 시간나면 구현할것");
            }
        });
        this.btnChoice=document.getElementById("btn-choice");
        this.btnChoice.addEventListener("click",()=>{
            if(window.role!="admin"){
                alert(`you are ${window.role}. not admin !`);
            }else{
                alert("일단은 다운로드만 쓰자. 업로드는 나중에 시간나면 구현할것");
            }
        });
        this.btnUpload=document.getElementById("btn-upload");
        this.btnUpload.addEventListener("click",()=>{
            if(window.role!="admin"){
                alert(`you are ${window.role}. not admin !`);
            }else{
                alert("일단은 다운로드만 쓰자. 업로드는 나중에 시간나면 구현할것");
            }
        });

    }
}

document.addEventListener("DOMContentLoaded", init);

async function init() {
    console.log("불러옴");

    // 태그들 세팅
    PAGE.init();


    // 파일 목록 가져오기
    getFileList("root");
}


async function getFileList(name) {
    try{
        if(name=="root"){
            PAGE.currentPath=[];
        }else if(name==".."){
            PAGE.currentPath.pop();
        }else{
            PAGE.currentPath.push(name);
        }

        const path = PAGE.currentPath.join("/");
        PAGE.spanPath.innerHTML="root/"+path;

        const resp = await fetch(`/files/search/${path||"root"}`);
        if(!resp.ok){ throw new Error("파일 리스트 가져오는데 실패"); }
        const respData = await resp.json();
        console.log(respData);

        const dirList = respData.dir_list;
        const fileList = respData.file_list;

        console.log("dir : ",dirList);
        console.log("file : ",fileList);

        // 상위로 이동
        PAGE.divDir.innerHTML = "";
        if(PAGE.currentPath.length>0){
            const a = document.createElement("a");
            a.classList.add("a-dir");

            // 이미지
            const img = document.createElement("img");
            img.src = "/static/image/up_img.png";
            img.alt = "Up Icon";
            a.appendChild(img);

            // 텍스트 노드로 파일 이름 추가
            const textNode = document.createTextNode("..");
            a.appendChild(textNode);

            a.href = "#";
            a.onclick = (evt)=>{
                evt.preventDefault();
                getFileList("..");
            };
            PAGE.divDir.appendChild(a);
        }
        // 디렉터리 표시
        dirList.forEach(f =>{
            const a = document.createElement("a");
            a.classList.add("a-dir");

            // 이미지
            const img = document.createElement("img");
            img.src = "/static/image/dir_img.png";
            img.alt = "Dir Icon";
            a.appendChild(img);

            // 텍스트 노드로 파일 이름 추가
            const textNode = document.createTextNode(f);
            a.appendChild(textNode);


            a.href = "#";
            a.onclick = (evt)=>{
                evt.preventDefault();
                getFileList(f);
            }            
            PAGE.divDir.appendChild(a);
        });
        // 파일 표시
        PAGE.divFile.innerHTML = "";
        fileList.forEach(f =>{
            const a = document.createElement("a");
            a.classList.add("a-file");

            // 이미지 추가
            const img = document.createElement("img");
            img.src = "/static/image/file_img.png";
            img.alt = "File Icon";
            a.appendChild(img);

            // 텍스트 노드로 파일 이름 추가
            const textNode = document.createTextNode(f);
            a.appendChild(textNode);

            const downloadPath = path ? `${path}/${f}` : f; // 경로가 비어있을 때 파일 이름만 사용
            a.href = `/files/download/${downloadPath}`;

            PAGE.divFile.appendChild(a);
        });


    }catch(e){
        console.log("ERROR from getFileList : ",e);
        alert("ERROR from getFileList");
    }

}
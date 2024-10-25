// files.js

const PAGE = {
    currentPath:[],
    secDir:null,
    secFile:null,
    init:function(){
        this.secDir=document.getElementById("dir");
        this.secFile=document.getElementById("file");
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
        const resp = await fetch(`/files/search/${path||"root"}`);
        if(!resp.ok){ throw new Error("파일 리스트 가져오는데 실패"); }
        const respData = await resp.json();
        console.log(respData);

        const dirList = respData.dir_list;
        const fileList = respData.file_list;

        console.log("dir : ",dirList);
        console.log("file : ",fileList);

        // 상위로 이동
        PAGE.secDir.innerHTML = "";
        if(PAGE.currentPath.length>0){
            const a = document.createElement("a");
            a.href = "#";
            a.textContent = "..";
            a.onclick = (evt)=>{
                evt.preventDefault();
                getFileList("..");
            };
            PAGE.secDir.appendChild(a);
            PAGE.secDir.appendChild(document.createElement("br"));
        }
        // 디렉터리 표시
        dirList.forEach(f =>{
            const a = document.createElement("a");
            a.href = "#";
            a.textContent = f;
            a.onclick = (evt)=>{
                evt.preventDefault();
                getFileList(f);
            }            
            PAGE.secDir.appendChild(a);
            PAGE.secDir.appendChild(document.createElement("br"));
        });
        // 파일 표시
        PAGE.secFile.innerHTML = "";
        fileList.forEach(f =>{
            const a = document.createElement("a");
            const downloadPath = path ? `${path}/${f}` : f; // 경로가 비어있을 때 파일 이름만 사용
            a.href = `/files/download/${downloadPath}`;
            a.textContent = f;
            PAGE.secFile.appendChild(a);
            PAGE.secFile.appendChild(document.createElement("br"));
        });


    }catch(e){
        console.log("ERROR from getFileList : ",e);
        alert("ERROR from getFileList");
    }

}
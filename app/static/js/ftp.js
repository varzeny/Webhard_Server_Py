// ftp.js

const PAGE = {
    btnTest:null,
    onoff:null,
    init:function(){
        this.onoff = document.getElementById("onoff");
        this.onoff.addEventListener("change",function(){
            const isChecked = this.checked;

            // 서버에 상태 전송
            fetch('/ftp/onoff', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ checked: isChecked })
            }).then(response => {
              if (response.ok) {
                console.log("서버에 전송 성공!");
              } else {
                console.error("전송 실패.");
              }
            }).catch(error => console.error("에러 발생:", error));
        });

        // test
        this.btnTest = document.getElementById("btn-test");
        this.btnTest.addEventListener("click", function(){
          console.log("테스트 버튼 눌림");
            fetch("/ftp/test", {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({ "val1":true })
            }).then(response=>{
                if (response.ok) {
                    console.log("서버에 전송 성공!");
                  } else {
                    console.error("전송 실패.");
                  }
            }).catch(error => console.error("에러 발생:", error));
        });

        checkStatus();


    }
}


document.addEventListener("DOMContentLoaded", init);

async function init() {
    console.log("로드 완료");

    // page init
    PAGE.init();
    // test();

}

async function checkStatus() {
  try{
    const resp = await fetch("/ftp/status");
    if(!resp.ok){ throw Error("FTP서버 상태 확인이 안됨"); }

    const respData = await resp.json();
    console.log("FTP서버로부터 상태 응답 받음 :", respData);

    PAGE.onoff.checked = respData.onoff;
  }catch(error){
    console.log("ERROR from checkStatus : ", error);
  }
}


// async function test() {
//     console.log("ttttttttt");
//     const resp = await fetch("/ftp/onoff",{
//         method:"POST",
//         headers:{ "Content-Type": "application/json" },
//         body:JSON.stringify({ "onoff": true })
//     });
//     if(!resp.ok){ throw Error("FTP서버 상태 확인이 안됨"); }
//     const respData = await resp.json();
//     console.log("!!!");
//     PAGE.onoff.checked = respData.onoff;

// }
const availableLanguages = ['zh-TW','en','de','fr','es','ko','ja','pt','vi','th'];
const defaultLanguages = ['zh-TW', 'en'];
const allCountries = ['US', 'FR', 'JP', 'KR', 'TW', 'GB', 'DE', 'ES', 'PT', 'VN', 'TH', 'CN', 'GL', 'CA', 'MX', 'BR', 'AR', 'PE', 'CL', 'TR', 'SA', 'IR', 'IQ', 'SY', 'AF', 'ZA', 'EG', 'MG', 'LT', 'UA', 'NO', 'SE', 'FI', 'IT', 'GR', 'PL', 'BY', 'RU', 'IN', 'PK', 'MM', 'MY', 'ID', 'PH', 'AU', 'NZ', 'SD', 'SS', 'MA', 'NG', 'CD', 'DZ', 'KZ', 'PG', 'LA', 'KH', 'IE', 'NL', 'BE', 'BO', 'DK', 'NI', 'UZ', 'NP', 'BD', 'LY', 'CF', 'YE', 'OM', 'CO', 'VE', 'GH', 'CI', 'IS', 'ZM', 'MR', 'KE', 'ML', 'NA', 'AO', 'CG', 'MN', '_0', '_1', '_2', 'AE', 'AL', 'AM', 'AT', 'AZ', 'BA', 'BF', 'BG', 'BI', 'BJ', 'BN', 'BS', 'BT', 'BW', 'BZ', 'CH', 'CM', 'CR', 'CU', 'CY', 'CZ', 'DJ', 'DO', 'EC', 'EE', 'EH', 'ER', 'ET', 'FJ', 'FK', 'GA', 'GE', 'GM', 'GN', 'GQ', 'GT', 'GW', 'GY', 'HN', 'HR', 'HT', 'HU', 'IL', 'JM', 'JO', 'KG', 'KP', 'KW', 'LB', 'LK', 'LR', 'LS', 'LU', 'LV', 'MD', 'ME', 'MK', 'MW', 'MZ', 'NC', 'NE', 'PA', 'PR', 'PS', 'PY', 'QA', 'RO', 'RS', 'RW', 'SB', 'SI', 'SK', 'SL', 'SN', 'SO', 'SR', 'SV', 'TD', 'TG', 'TJ', 'TM', 'TN', 'TT', 'TZ', 'UG', 'UY', 'ZW', 'SG'];
const defaultCountries = ["TW","JP","KR","CN","FR","RU","US","GB"];
const pleaseSearch = {"zh-TW":"   請輸入...","en":"   Search...","de":"   Suchbegriff eingeben...","fr":"   Recherche...","es":"   Buscar...","ko":"   검색어를 입력해 주세요...","ja":"   検索...","pt":"   Pesquisa...","vi":"   Tìm kiếm...","th":"   พิมพ์คำค้นหา...",};
const monthMap = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"};

var separateLine = document.createElement("hr");
separateLine.setAttribute("class","separate-line");
var newsContent = {} //新聞內容放的位置
var userLanguage = 'zh-TW';
var selectedCountries = [];
var dirty = false;

// 顯示新聞框框的內容
function showContent(code, mode){
    let outHTML = ''

    // 國家名稱
    let name_div = document.createElement("div");
    let name_p = document.createElement("p");
    name_p.setAttribute("class", "inline country");
    name_p.appendChild(document.createTextNode(countriesNames[code][userLanguage]));
    name_div.appendChild(name_p);
    
    // 比較區塊的移除圖案
    if(mode=="compare"){
        let remove_div = document.createElement("div");
        remove_div.setAttribute("class","remove inline");
        let img = document.createElement("img");
        img.setAttribute("src","./static/image/cross.png");
        img.setAttribute("id","remove"+code);
        img.setAttribute("onclick","removeComparison(this)");
        remove_div.appendChild(img);
        name_div.appendChild(remove_div);
    }

    name_div.appendChild(separateLine);

    outHTML += name_div.outerHTML;

    let ele = this["map"]["regions"][code]["element"];

    if(ele.isSearched==false&&dirty==true){return outHTML;}

    if(ele.isPending){return outHTML;}

    
    // 新聞標題
    for(let i in newsContent[code]){
        
        let obj = newsContent[code][i];
        if(obj["original"]==""){continue;}
        if(obj[userLanguage]==""){continue;}

        let divi = document.createElement("div");
        let hrefi = document.createElement("a");
        let titlei = document.createElement("p");
        
        hrefi.setAttribute("href",obj["href"]);
        hrefi.setAttribute("target","_blank");
        titlei.setAttribute("class","news_title");
        titlei.innerText = obj[userLanguage];

        hrefi.appendChild(titlei);
        divi.appendChild(hrefi);
        divi.appendChild(separateLine);
        outHTML += divi.outerHTML;
    }

    return outHTML;
}

// 使用者點選國家
function showComparison(code, isSelected){

    if(isSelected){
        selectedCountries.push(code);
    }else{
        selectedCountries.splice(selectedCountries.indexOf(code), 1);
    }

    // 處理地圖顏色
    __colorMap();

    // 更新比較區塊
    __refreshComparisonArea();
}

function doSearch(){

    dirty = true;
    let searchCountries = (selectedCountries.length>0)? selectedCountries: defaultCountries;
    setPending(searchCountries);
    __refreshComparisonArea();
    
    let keyword = document.getElementById("searchField").value;

    for(let x in searchCountries){

        let code = searchCountries[x];

        let ele = this["map"]["regions"][code]["element"];
        ele.isSearched = true;

        $.ajax({
            type: "GET",
            url: "http://localhost:8000",
            crossDomain: true,
            cache: true,
            data: {
                "method":"keyword",
                "countries":[code].toString(),
                "user_language":userLanguage,
                "keyword":keyword,
            },
            dataType: 'json',
            timeout: 300000,
            success: function (result, status, xhr){
                console.log(result);
                for(let res in result){
                    newsContent[res] = result[res];
                    unsetPending([res]);
                }
            },
            error: function(xhr){
                console.log(code + ": statusText="+xhr.statusText);
            }
        });
    }
}

// 一開網頁時跟server要首頁內容
$(document).ready(function(){
    $.ajax({
        type: "GET",
        url: "http://localhost:8000",
        crossDomain: true,
        cache: true,
        data: {
            "method":"homepage",
            "countries":allCountries.toString(),
            "user_language":userLanguage,
            "keyword":[].toString(),
        },
        dataType: 'json',
        timeout: 10000,
        success: function (result, status, xhr){
            newsContent = result;
        },
        error: function(xhr){
          alert("statusText="+xhr.statusText);
        }
    });
});

// 使用者下拉選單切換語言
function changeLanguage(language){

    userLanguage = language.value;

    // search bar 請輸入的文字
    document.getElementById("searchField").placeholder = pleaseSearch[userLanguage];

    if(dirty){
        for(let index in allCountries){
            let code = allCountries[index];
            let ele = this["map"]["regions"][code]["element"];
            if(ele.isSearched){
                __translateNews(code);
            }
        }
    }else{
        // 先翻譯有被放入比較區塊的國家
        for(let selected in selectedCountries){
            let code = selectedCountries[selected];
            __translateNews(code);
        }
        // 再翻其他剩餘的國家
        for(let code in newsContent){
            if(selectedCountries.includes(code)){continue;}
            __translateNews(code);
        }
    }
    
}

// 塗成橘色
function setPending(countriesList){
    for(let i in allCountries){
        let code = allCountries[i];
        let ele = this["map"]["regions"][code]["element"];
        ele.isSearched = false;
    }
    for(let i in countriesList){
        let code = countriesList[i];
        let ele = this["map"]["regions"][code]["element"];
        ele.isSearched = true;
        ele.isPending = true;
    }
    __colorMap();
}

function unsetPending(countriesList){

    // 將已完成搜尋的pending狀態設為false
    for(let i in countriesList){
        
        let code = countriesList[i];
        let ele = this["map"]["regions"][code]["element"];
        ele.isPending = false;

        if(selectedCountries.includes(code)){__refreshComparisonArea();}

        __colorMap();

    }

}

function refreshPage(){
    window.location.reload();
}

function __searchNewsIndex(code, original){
    for(let dict_index in newsContent[code]){
        if(newsContent[code][dict_index]["original"]==original){
            return dict_index;
        }
    }
    return -1;
}

function __colorMap(){
    for(let index in allCountries){
        let code = allCountries[index];
        let ele = this["map"]["regions"][code]["element"];

        if(ele.isPending){
            ele.setStyle("fill","orange");
            ele.setStyle("fillOpacity",0.7);
        }else{
            if(ele.isSelected){
                ele.setStyle("fill","#72bbbb");
                ele.setStyle("fillOpacity",1);
            }else{
                if(ele.isSearched){
                    ele.setStyle("fill","#A9E3E3");
                    ele.setStyle("fillOpacity",1);
                }else{
                    ele.setStyle("fill","#beddd7");
                    ele.setStyle("fillOpacity",0.8);
                }
            }
        }
    }
}

function __refreshComparisonArea(){
    let block = document.getElementById("compareArea");
    block.innerHTML = "";
    for(let i=selectedCountries.length-1; i>=0; i--){
        let div = document.createElement("div");
        div.setAttribute("class","jsvmap-tooltip-another");
        div.style.float="left";
        div.innerHTML = showContent(selectedCountries[i], "compare");
        block.appendChild(div);
    }
}

function __translateNews(code){
    let news_dict_list = newsContent[code];

    let to_translate = "";
    for(let index in news_dict_list){
        news_dict = news_dict_list[index];
        if(news_dict["original"]==""){continue;}
        if(news_dict[userLanguage]!=""){
            __refreshComparisonArea();
            continue;
        }
        to_translate += news_dict["original"] + "+";
    }
    // 移除最後一個+
    to_translate = to_translate.substring(0, to_translate.length - 1);
    if(to_translate.length==0){return;}

    $.ajax({
        type: "GET",
        url: "http://localhost:8000",
        crossDomain: true,
        cache: true,
        data: {
            "method":"translate",
            "countries":[code].toString(),
            "user_language":userLanguage,
            "text":to_translate,
        },
        dataType: 'json',
        timeout: 300000,
        success: function (result, status, xhr){
            let result_dict_list = result[code];
            for(let index in result_dict_list){
                result_dict = result_dict_list[index];
                
                let news_index = __searchNewsIndex(code, result_dict['original']);

                newsContent[code][news_index][userLanguage] = result_dict['translated'];
            }
            if(selectedCountries.includes(code)){__refreshComparisonArea();}
        },
        error: function(xhr){
            console.log(code + ": statusText="+xhr.statusText);
        },
    });
}

function removeComparison(ele){
    let code = ele.id.substring(6,8);
    let regionEle = this["map"]["regions"][code]["element"];
    regionEle.deselect();
    selectedCountries.splice(selectedCountries.indexOf(code), 1);
    __colorMap();
    __refreshComparisonArea();
}

function viewHistory(){
    let ele = document.getElementById("myCalendarWrapper");
    if(ele.style.display=="block"){
        ele.style.display = "none";
    }else{
        ele.style.display = "block";
    }
}

var myCalender = new CalendarPicker('#myCalendarWrapper', {
    min: new Date(2022,7,3),
    max: new Date(), 
    locale: 'zh-TW', // Can be any locale or language code supported by Intl.DateTimeFormat, defaults to 'en-US'
    showShortWeekdays: false // Can be used to fit calendar onto smaller (mobile) screens, defaults to false
});

function __parseDate(date){

    //date格式：Thu Aug 11 2022
    let temp = date.split(" ");
    let out = temp[3] + "-" + monthMap[temp[1]] + "-" + temp[2];
    return out;

}

myCalender.onValueChange((currentValue) => {

    document.getElementById("myCalendarWrapper").style.display = "none";

    //currentValue.toDateString()格式：Thu Aug 11 2022
    let parsedDate = __parseDate(currentValue.toDateString());
    
    $.ajax({
        type: "GET",
        url: "http://localhost:8000",
        crossDomain: true,
        cache: true,
        data: {
            "method":"history",
            "countries":allCountries.toString(),
            "user_language":userLanguage,
            "keyword":[parsedDate].toString(),
        },
        dataType: 'json',
        timeout: 10000,
        success: function (result, status, xhr){
            newsContent = result;
        },
        error: function(xhr){
          alert("statusText="+xhr.statusText);
        }
    });
    
    
});

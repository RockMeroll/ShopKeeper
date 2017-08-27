var type = ['', 'info', 'success', 'warning', 'danger'];


var demo = {
    initChartist: function () {
        var optionsSales = {
            lineSmooth: false,
            low: 0,
            high: 800,
            showArea: true,
            height: "245px",
            axisX: {
                showGrid: false,
            },
            showLine: false,
            showPoint: false,
        };
    }
};

chartinit();

function createXMLRequest() {
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHttp");
    }
}

function getChartDate(year, month, day) {
    var url = window.location.host;
    // xmlhttp.onreadystatechange = function () {
    //     if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
    //         document.getElementById("chartFlow").innerHTML = xmlhttp.responseText;
    //     }
    // }
    var getUrl = "/get_result/";
    createXMLRequest();
    xmlhttp.open("POST", getUrl, false);
    xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xmlhttp.send("year=2017&month=4&day=1");
    return xmlhttp.responseText
}

function updateLine(result, labels, id) {
    var data = {
            labels: labels,
            series: result
        },
        options = {
            lineSmooth: false,
            low: 0,
            high: Math.max.apply(null, result),
            showArea: true,
            height: "245px",
            axisX: {
                showGrid: false
            },
            showLine: false,
            showPoint: false
        },
        responsive = [
            ['screen and (max-width: 640px)', {
                axisX: {
                    labelInterpolationFnc: function (value) {
                        return value[0];
                    }
                }
            }]
        ];

    new Chartist.Line("#" + id, data, options, responsive);
}


function updatePie(result, id) {
    var sum = result[0];
    result.splice(0, 1);
    var label = [];
    for (var i in result) {
        var rate = result[i] / sum;
        label.push(rate.toFixed(2) * 100 + "%");
    }
    var data = {
        labels: label,
        series: result
    };

    var options = {
        total: sum,
        showLabel: true
    };
    new Chartist.Pie("#" + id, data, options);
}

function parseData(json_str) {
    var json_data = JSON.parse(json_str);
    var splited_data = [];
    splited_data["flow"] = [];
    splited_data["inner"] = [];
    splited_data["new"] = [];
    splited_data["old"] = [];
    labels = [];

    for (var key in json_data) {
        if (key != "sum") {
            labels.push(parseInt(key));
            splited_data["flow"].push(parseInt(json_data[key][1]));
            splited_data["inner"].push(parseInt(json_data[key][2]));
            splited_data["new"].push(parseInt(json_data[key][5]));
            splited_data["old"].push(parseInt(json_data[key][6]));
        }
    }

    var result = [];
    result["splited_data"] = splited_data;
    result["flow"] = json_data["sum"][1];
    result["inner"] = json_data["sum"][2];
    result["outer"] = json_data["sum"][3];
    result["deepin"] = json_data["sum"][4];
    return result;
}

function chartSet(year, month, day) {
    var url = window.location.host;
    createXMLRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var result = parseData(xmlhttp.responseText);
            updateLine([result["splited_data"]["flow"]], labels, "chartFlow");
            updateLine([result["splited_data"]["inner"]], labels, "chartInner");
            updateLine([result["splited_data"]["new"]], labels, "chartNew");
            updateLine([result["splited_data"]["old"]], labels, "chartOld");
            updatePie([result['flow'], result['inner']], "chartInnerRate");
            updatePie([result['flow'], result['outer']], "chartOuterRate");
            updatePie([result['flow'], result['deepin']], "chartDeepInRate");
        }
    };
    var getUrl = "/get_result/";
    xmlhttp.open("POST", getUrl, true);
    xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    if(day == "all"){
        xmlhttp.send("year=" + year + "&month=" + month);
    }else {
        xmlhttp.send("year=" + year + "&month=" + month + "&day=" + day);
    }
}

function chartinit() {
    chartSet(2017,4,7);
}

function inquiry(){

    var year = $('#year option:selected').text().trim();

    var month = $('#month option:selected').text().trim();

    var day = $('#day option:selected').text().trim();

    chartSet(year,month,day);
}

function compare(){
    var year1 = $('#c1-year option:selected').text().trim();

    var month1 = $('#c1-month option:selected').text().trim();

    var day1 = $('#c1-day option:selected').text().trim();

    createXMLRequest();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var result1 = parseData(xmlhttp.responseText);

            var year2 = $('#c2-year option:selected').text().trim();

            var month2 = $('#c2-month option:selected').text().trim();

            var day2 = $('#c2-day option:selected').text().trim();
            
            createXMLRequest();
            xmlhttp.onreadystatechange = function (){
                var result2 = parseData(xmlhttp.responseText);
                updateLine([result1["splited_data"]["flow"],result2["splited_data"]["flow"]], labels, "chartFlow");
                updateLine([result1["splited_data"]["inner"], result2["splited_data"]["inner"]], labels, "chartInner");
                updateLine([result1["splited_data"]["new"],result2["splited_data"]["new"]], labels, "chartNew");
                updateLine([result1["splited_data"]["old"],result2["splited_data"]["old"]], labels, "chartOld");
                updatePie([result1['flow']+result2['flow'], result1['inner'],result2['inner']], "chartInnerRate");
                updatePie([result1['flow']+result2['flow'], result1['outer'],result2['outer']], "chartOuterRate");
                updatePie([result1['flow']+result2['flow'], result1['deepin'], result2['deepin']], "chartDeepInRate");

            };
            xmlhttp.open("POST", getUrl, true);
            xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            if(day2 == "all"){
                xmlhttp.send("year=" + year2 + "&month=" + month2);
            }else {
                xmlhttp.send("year=" + year2 + "&month=" + month2 + "&day=" + day2);
            }

        }
    };
    var getUrl = "/get_result/";
    xmlhttp.open("POST", getUrl, true);
    xmlhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    if(day1 == "all"){
        xmlhttp.send("year=" + year1 + "&month=" + month1);
    }else {
        xmlhttp.send("year=" + year1 + "&month=" + month1 + "&day=" + day1);
    }
}


var NetworkVisualization = function (data) {
    this.data = data;
    this.networks = ["OTHER", "RTT", "CDMA", "EDGE", "EHRPD", "EVDO_0", "EVDO_A", "EVDO_B", "GPRS", "HSDPA", "HSPA", "HSPAP", "HSUPA", "IDEN", "LTE", "UMTS", "UNKNOWN"];
    this.groupColor = {
        "2G": "#0000FF",
        "3G": "#008000",
        "4G": "#FF4500",
    };
    this.groupData = {};
    this.markerColor;
    var max = 0;
    for (var network in data) {
        group = this.codeToGroup(network);
        if (group in this.groupData) {
            this.groupData[group] = this.groupData[group] + data[network];
        }
        else {
            this.groupData[group] = data[network];
        }
        if (group in this.groupColor && this.groupData[group] > max){
            max = this.groupData[group];
            this.markerColor = this.groupColor[group];
        }
    }
};

NetworkVisualization.prototype.codeToName = function (code) {
    return this.networks[code];
};

NetworkVisualization.prototype.codeToGroup = function (code) {
    networkType = this.codeToName(code);
    switch (networkType) {
        case "GPRS":
        case "EDGE":
        case "CDMA":
        case "RTT":
        case "IDEN":
            return "2G";
        case "UMTS":
        case "EVDO_0":
        case "EVDO_A":
        case "HSDPA":
        case "HSUPA":
        case "HSPA":
        case "EVDO_B":
        case "EHRPD":
        case "HSPAP":
            return "3G";
        case "LTE":
            return "4G";
        default:
            return networkType;
    }
};

NetworkVisualization.prototype.getDataChart = function () {
    ans = [];
    $.each(this.groupData, function (group, quantity) {
        ans.push([group, quantity]);
    });
    return ans;
};

NetworkVisualization.prototype.getColorChart = function () {
    return this.groupColor;
};

NetworkVisualization.prototype.getColorMarker = function () {
    return this.markerColor;
};

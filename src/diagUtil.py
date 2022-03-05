def aggregateSeries(datapoint, groupCount):
    """
    Aggregate a list of datapoints into a series of aggregated datapoints.
    """
    groupSize = len(datapoint) // groupCount
    if len(datapoint) < groupCount:
        return [datapoint]
    else:
        return [
            sum(datapoint[i : i + groupSize]) / groupSize
            for i in range(0, len(datapoint), groupSize)
        ]

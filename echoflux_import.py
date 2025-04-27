from chrono_keys import ChronoKey, echoflux_import

keys = [ChronoKey("Kairos"), ChronoKey("Aion"), ChronoKey("Eternity")]
imported_data = echoflux_import(
    timestream_id=8745213,
    dimensional_offset=4.7231,
    chrono_keys=keys
)

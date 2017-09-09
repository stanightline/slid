<?php session_start();

include "../utils.php";

if (is_logged_in()) {
    // load existing data
    $id = $_POST["id"];
    $inp = get_with_backup();
    $tempArray = json_decode($inp);

    // iterate to delete existing
    $i = 0;
    foreach ($tempArray as $element) {
        // check the id of every element
        if ($element->id == $id) {
            unset($tempArray[$i]);
            break;
        }
        $i++;
    }

    // push and save new array
    $jsonData = json_encode($tempArray, JSON_UNESCAPED_SLASHES);

    // save the modified data
    file_put_contents("../../misc/info.json", $jsonData);

    // tell the user we're done
    echo "SUCCESS";
} else {
    echo "CARD DELETION FAILURE: You must be logged in!";
}

// and die
die();

{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNxCgvtXQD/Z7L66zrsc4SK",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/JanaviSanthosh/nie_med_74_cse_fastapi/blob/main/main.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from fastapi import FastAPI, HTTPException\n",
        "from pydantic import BaseModel\n",
        "\n",
        "from pymongo import MongoClient\n",
        "from bson import ObjectId\n",
        "\n",
        "# app\n",
        "app = FastAPI()\n",
        "\n",
        "# db config\n",
        "URL = \"mongodb://127.0.0.1:27017\"\n",
        "client = MongoClient(URL)\n",
        "db = client[\"service_ticket_db\"]\n",
        "ticket_collection = db[\"tickets\"]\n",
        "\n",
        "# schema pydantic\n",
        "class TicketCreate(BaseModel):\n",
        "    title: str\n",
        "    description: str\n",
        "    category: str\n",
        "    status: str\n",
        "\n",
        "class TicketResponse(TicketCreate):\n",
        "    id: str\n",
        "\n",
        "# helper\n",
        "def ticket_helper(ticket_doc):\n",
        "    return {\n",
        "        \"id\": str(ticket_doc[\"_id\"]),\n",
        "        \"title\": str(ticket_doc[\"title\"]),\n",
        "        \"description\": str(ticket_doc[\"description\"]),\n",
        "        \"status\": str(ticket_doc[\"status\"]),\n",
        "}\n",
        "\n",
        "# apis - CRUD - create,read all, read by id,update, delete\n",
        "@app.post(\"/tickets\", status_code=201, response_model=TicketResponse)\n",
        "def ticket_create(payload: TicketCreate):\n",
        "    ticket_dict = payload.model_dump()\n",
        "    result = ticket_collection.insert_one(ticket_dict)\n",
        "    new_ticket = ticket_collection.find_one({\"_id\": result.inserted_id})\n",
        "    return ticket_helper(new_ticket)\n",
        "\n",
        "\n",
        "@app.get(\"/tickets\", response_model=list[TicketResponse])\n",
        "def ticket_read_all():\n",
        "    docs = ticket_collection.find()\n",
        "    tickets = [ticket_helper(doc) for doc in docs]\n",
        "    return tickets\n",
        "\n",
        "@app.get(\"/tickets/{id}\", response_model=TicketResponse)\n",
        "def ticket_read_by_id(id: str):\n",
        "    if not ObjectId.is_valid(id):\n",
        "        raise HTTPException(detail=\"Invalid ticket ID\",status_code=403)\n",
        "    doc = ticket_collection.find_one({\"_id\": ObjectId(id)})\n",
        "    if not doc:\n",
        "        raise HTTPException(detail=\"Ticket not found\", status_code=404)\n",
        "    return ticket_helper(doc)\n",
        "\n",
        "@app.put(\"/tickets/{id}\", response_model=TicketResponse)\n",
        "def ticket_update(id: str, payload: TicketCreate):\n",
        "    if not ObjectId.is_valid(id):\n",
        "        raise HTTPException(detail=\"Invalid ticket ID\", status_code=403)\n",
        "    ticket_dict = payload.model_dump()\n",
        "    result = ticket_collection.update_one({\"_id\": ObjectId(id)}, {\"$set\": ticket_dict})\n",
        "    if result.matched_count == 0:\n",
        "        raise HTTPException(detail=\"Ticket not found\", status_code=404)\n",
        "    new_ticket = ticket_collection.find_one({\"_id\": ObjectId(id)})\n",
        "    return ticket_helper(new_ticket)\n",
        "\n",
        "@app.delete(\"/tickets/{id}\")\n",
        "def ticket_delete(id: str):\n",
        "    if not ObjectId.is_valid(id):\n",
        "        raise HTTPException(detail=\"Invalid ticket ID\", status_code=403)\n",
        "    result = ticket_collection.delete_one({\"_id\": ObjectId(id)})\n",
        "    if result.deleted_count == 0:\n",
        "        raise HTTPException(detail=\"Ticket not found\", status_code=404)\n",
        "    return {\"message\": \"Ticket deleted successfully\"}\n",
        "\n",
        "\n",
        "\n",
        "\n",
        ""
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 383
        },
        "id": "pXi6O1osss88",
        "outputId": "d2625db9-7d39-4b1e-9e7a-8e2de266df5a"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "error",
          "ename": "ModuleNotFoundError",
          "evalue": "No module named 'pymongo'",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipykernel_757/377677908.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      2\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mpydantic\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mBaseModel\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 4\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0mpymongo\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mMongoClient\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      5\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mbson\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mObjectId\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      6\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'pymongo'",
            "",
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0;32m\nNOTE: If your import is failing due to a missing package, you can\nmanually install dependencies using either !pip or !apt.\n\nTo view examples of installing some common dependencies, click the\n\"Open Examples\" button below.\n\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n"
          ],
          "errorDetails": {
            "actions": [
              {
                "action": "open_url",
                "actionText": "Open Examples",
                "url": "/notebooks/snippets/importing_libraries.ipynb"
              }
            ]
          }
        }
      ]
    }
  ]
}
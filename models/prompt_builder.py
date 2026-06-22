def build_prompt(materials):

    material_list = "\n".join(
        [f"- {item}" for item in materials]
    )

    prompt = f"""
       You are a sustainability expert and DIY project designer.

       Available Waste Materials:

       {material_list}

       Your task:

       Generate ONE creative, useful and eco-friendly DIY project.

       Return the response in the following format:

       Project Name:
        <project name>

       Description:
        <short description>

       Difficulty:
        Easy / Medium / Hard

       Build Time:
       <estimated time>

       Materials:
       <list>

       Steps:
       1.
       2.
       3.
       4.
       5.

       Safety Tips:
        <tips>

       Rules:

        - Project must be practical.
        - Project should reuse maximum waste.
        - Project should be beginner friendly.
        - Steps must be clear.
        - Avoid dangerous projects.
        """

    return prompt